// dashboard home page
import React from "react";
import Info from "../components/Info";
import { useParams } from 'react-router-dom';

const Home = () => {

  const { component } = useParams();
  
  return (
    <>
      <Info component={component} />
    </>
  );
};

export default Home;
