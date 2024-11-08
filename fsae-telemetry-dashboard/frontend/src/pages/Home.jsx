// Home.jsx
import React, { useState } from "react";
import { 
  Flex, 
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Center,
  Text,
} from "@chakra-ui/react";

import { useParams } from 'react-router-dom';
import Databox from "../components/Databox";
import LineChart from "../components/Chart";
import Config from "../components/Config";
import Header from "../components/Header";

function Home() {
  const { extension } = useParams();
  const component = extension ? extension.charAt(0).toUpperCase() + extension.slice(1) : '';
  const margin = "1.0rem";

  const [selectedConfig, setSelectedConfig] = useState(null); // State for selected config values

  const handleConfigSelectionChange = (selectedOptions) => {
    setSelectedConfig(selectedOptions); // Update the selected config options
  };

  return (
    <Flex
      direction="column" 
      width="100%" 
      height="100vh" 
      bg="white"
      margin="0"
      padding="0"
    >
      <Header />

      {/* Main Content Area */}


      <Flex
        direction="column" 
        flex="1" 
        border="1px solid grey" 
        padding={margin}
      >
        {/* Title */}
        <Text fontSize="1.25rem" margin={margin}>
          {component} Management
        </Text>

          {/* Config Component */}
        <Config onChange={handleConfigSelectionChange} /> {/* Pass handler to Config */}

       
        <Center
          border="1px solid grey"
          padding="0.5rem"
          width="auto"
          flex="1"
          margin={margin}
          maxHeight="100.0rem"
        >
          <LineChart selectedConfig={selectedConfig} /> {/* Pass selectedConfig to LineChart */}
        </Center>
      </Flex>
    </Flex>
  );
}

export default Home;
