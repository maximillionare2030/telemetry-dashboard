// dashboard home page
import React from "react";
import Header from "../components/Header";
import { useParams } from 'react-router-dom';

const Home = () => {

  const { component } = useParams();
  return (
    <>
      <Header component={component} />
    </>
  );
};

export default Home;
