import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();
  // Redirect to welcome screen
  navigate("/");
  return null;
};

export default Index;
