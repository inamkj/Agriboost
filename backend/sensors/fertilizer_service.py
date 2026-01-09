"""
Fertilizer prediction service based on sensor readings.

This service uses sensor data (NPK values, pH, moisture, etc.) to recommend
appropriate fertilizers for optimal crop growth.
"""

from typing import Dict, List, Optional
import math


class FertilizerPredictionService:
    """
    Service for predicting fertilizer recommendations based on sensor readings.
    
    Uses rule-based logic to recommend fertilizers based on:
    - NPK levels (Nitrogen, Phosphorus, Potassium)
    - Soil pH
    - Soil moisture
    - Temperature
    """
    
    # Optimal ranges for NPK values
    OPTIMAL_NITROGEN = 50.0  # ppm
    OPTIMAL_PHOSPHORUS = 30.0  # ppm
    OPTIMAL_POTASSIUM = 40.0  # ppm
    
    # Optimal pH range
    OPTIMAL_PH_MIN = 6.0
    OPTIMAL_PH_MAX = 7.5
    
    # Optimal moisture range
    OPTIMAL_MOISTURE_MIN = 40.0  # %
    OPTIMAL_MOISTURE_MAX = 70.0  # %
    
    @staticmethod
    def predict_fertilizer(
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        soil_ph: float,
        soil_moisture: float,
        temperature: float,
        ec: Optional[float] = None
    ) -> Dict:
        """
        Predict fertilizer recommendation based on sensor readings.
        
        Args:
            nitrogen: Nitrogen level in ppm
            phosphorus: Phosphorus level in ppm
            potassium: Potassium level in ppm
            soil_ph: Soil pH value
            soil_moisture: Soil moisture percentage
            temperature: Temperature in Celsius
            ec: Electrical Conductivity (optional)
        
        Returns:
            Dictionary with fertilizer recommendation details
        """
        
        # Calculate deficiencies
        n_deficit = FertilizerPredictionService.OPTIMAL_NITROGEN - nitrogen
        p_deficit = FertilizerPredictionService.OPTIMAL_PHOSPHORUS - phosphorus
        k_deficit = FertilizerPredictionService.OPTIMAL_POTASSIUM - potassium
        
        # Determine which nutrients are deficient
        n_deficient = n_deficit > 10
        p_deficient = p_deficit > 5
        k_deficient = k_deficit > 10
        
        # pH adjustment needed
        ph_low = soil_ph < FertilizerPredictionService.OPTIMAL_PH_MIN
        ph_high = soil_ph > FertilizerPredictionService.OPTIMAL_PH_MAX
        
        # Build recommendation
        recommendations = []
        fertilizers = []
        confidence = 0.8  # Base confidence
        
        # Determine primary fertilizer recommendation
        if n_deficient and p_deficient and k_deficient:
            # All three deficient - use balanced NPK fertilizer
            fertilizers.append({
                'name': 'NPK 19:19:19 (Balanced)',
                'amount': max(n_deficit, p_deficit, k_deficit) * 2,  # kg/hectare
                'priority': 'high',
                'reason': 'All NPK levels are below optimal'
            })
            recommendations.append("Apply balanced NPK fertilizer to address nitrogen, phosphorus, and potassium deficiencies.")
            
        elif n_deficient and p_deficient:
            # Nitrogen and Phosphorus deficient
            fertilizers.append({
                'name': 'NPK 20:20:0',
                'amount': max(n_deficit, p_deficit) * 2.5,
                'priority': 'high',
                'reason': 'Nitrogen and Phosphorus levels are below optimal'
            })
            recommendations.append("Apply NP fertilizer to address nitrogen and phosphorus deficiencies.")
            
        elif n_deficient and k_deficient:
            # Nitrogen and Potassium deficient
            fertilizers.append({
                'name': 'NPK 17:0:45',
                'amount': max(n_deficit, k_deficit) * 2.2,
                'priority': 'high',
                'reason': 'Nitrogen and Potassium levels are below optimal'
            })
            recommendations.append("Apply NK fertilizer to address nitrogen and potassium deficiencies.")
            
        elif p_deficient and k_deficient:
            # Phosphorus and Potassium deficient
            fertilizers.append({
                'name': 'NPK 0:20:20',
                'amount': max(p_deficit, k_deficit) * 2.3,
                'priority': 'high',
                'reason': 'Phosphorus and Potassium levels are below optimal'
            })
            recommendations.append("Apply PK fertilizer to address phosphorus and potassium deficiencies.")
            
        elif n_deficient:
            # Only Nitrogen deficient
            fertilizers.append({
                'name': 'Urea (46-0-0)',
                'amount': n_deficit * 2.2,
                'priority': 'high',
                'reason': 'Nitrogen level is below optimal'
            })
            recommendations.append("Apply nitrogen-rich fertilizer to address nitrogen deficiency.")
            
        elif p_deficient:
            # Only Phosphorus deficient
            fertilizers.append({
                'name': 'Single Super Phosphate (0-20-0)',
                'amount': p_deficit * 3.0,
                'priority': 'medium',
                'reason': 'Phosphorus level is below optimal'
            })
            recommendations.append("Apply phosphorus fertilizer to address phosphorus deficiency.")
            
        elif k_deficient:
            # Only Potassium deficient
            fertilizers.append({
                'name': 'Muriate of Potash (0-0-60)',
                'amount': k_deficit * 1.7,
                'priority': 'medium',
                'reason': 'Potassium level is below optimal'
            })
            recommendations.append("Apply potassium fertilizer to address potassium deficiency.")
            
        else:
            # All nutrients adequate
            fertilizers.append({
                'name': 'Maintenance Fertilizer (10:10:10)',
                'amount': 50.0,  # Maintenance dose
                'priority': 'low',
                'reason': 'All NPK levels are within optimal range'
            })
            recommendations.append("NPK levels are optimal. Apply maintenance fertilizer for sustained growth.")
            confidence = 0.9
        
        # pH adjustments
        if ph_low:
            fertilizers.append({
                'name': 'Lime (Calcium Carbonate)',
                'amount': (FertilizerPredictionService.OPTIMAL_PH_MIN - soil_ph) * 1000,  # kg/hectare
                'priority': 'high',
                'reason': f'Soil pH ({soil_ph:.2f}) is below optimal range. Apply lime to raise pH.'
            })
            recommendations.append(f"Apply lime to raise soil pH from {soil_ph:.2f} to optimal range (6.0-7.5).")
            confidence = 0.85
            
        elif ph_high:
            fertilizers.append({
                'name': 'Sulfur or Gypsum',
                'amount': (soil_ph - FertilizerPredictionService.OPTIMAL_PH_MAX) * 800,
                'priority': 'medium',
                'reason': f'Soil pH ({soil_ph:.2f}) is above optimal range. Apply acidifying agent.'
            })
            recommendations.append(f"Apply sulfur or gypsum to lower soil pH from {soil_ph:.2f} to optimal range (6.0-7.5).")
            confidence = 0.85
        
        # Moisture adjustments
        if soil_moisture < FertilizerPredictionService.OPTIMAL_MOISTURE_MIN:
            recommendations.append(f"Soil moisture ({soil_moisture:.1f}%) is low. Consider irrigation before fertilizer application.")
            confidence -= 0.05
        elif soil_moisture > FertilizerPredictionService.OPTIMAL_MOISTURE_MAX:
            recommendations.append(f"Soil moisture ({soil_moisture:.1f}%) is high. Wait for soil to dry slightly before application.")
            confidence -= 0.05
        
        # Temperature considerations
        if temperature < 15:
            recommendations.append("Temperature is low. Fertilizer uptake may be slower. Consider waiting for warmer conditions.")
            confidence -= 0.05
        elif temperature > 35:
            recommendations.append("Temperature is high. Avoid fertilizer application during peak heat. Apply early morning or evening.")
            confidence -= 0.05
        
        # Ensure confidence is within bounds
        confidence = max(0.5, min(0.95, confidence))
        
        # Primary fertilizer (highest priority)
        primary_fertilizer = max(fertilizers, key=lambda x: 1 if x['priority'] == 'high' else 0.5 if x['priority'] == 'medium' else 0.25) if fertilizers else None
        
        return {
            'recommended_fertilizer': primary_fertilizer['name'] if primary_fertilizer else 'No specific recommendation',
            'fertilizer_amount': round(primary_fertilizer['amount'], 2) if primary_fertilizer else 0,
            'confidence_score': round(confidence, 2),
            'recommendation_details': ' '.join(recommendations),
            'all_fertilizers': fertilizers,
            'deficiencies': {
                'nitrogen': round(n_deficit, 2) if n_deficit > 0 else 0,
                'phosphorus': round(p_deficit, 2) if p_deficit > 0 else 0,
                'potassium': round(k_deficit, 2) if k_deficit > 0 else 0
            },
            'status': {
                'nitrogen': 'deficient' if n_deficient else 'adequate',
                'phosphorus': 'deficient' if p_deficient else 'adequate',
                'potassium': 'deficient' if k_deficient else 'adequate',
                'ph': 'low' if ph_low else 'high' if ph_high else 'optimal',
                'moisture': 'low' if soil_moisture < FertilizerPredictionService.OPTIMAL_MOISTURE_MIN else 'high' if soil_moisture > FertilizerPredictionService.OPTIMAL_MOISTURE_MAX else 'optimal'
            }
        }




