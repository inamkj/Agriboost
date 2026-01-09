import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";
import LoaderOverlay from "../components/LoaderOverlay";

export default function Logout() {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
     
    
    const timer = setTimeout(() => navigate("/login"), 1500);
    logout();
    return () => clearTimeout(timer);
    
  }, [logout, navigate]);

  return <LoaderOverlay loading={true} message="Logging out..." />;
}
