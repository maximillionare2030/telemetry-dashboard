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
import 

import { useParams } from 'react-router-dom';
import LineChart from "../components/Chart";
import Config from "../components/Config";

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
      {/* Breadcrumb navigation */}
      <Flex
        as="nav"
        aria-label="breadcrumb"
        align="center"
        justify="space-between"
        wrap="wrap"
        border="1px solid grey"
      >
        <Breadcrumb separator="/" fontSize="1.25rem">
          {['Power', 'Motor', 'Microcontroller'].map((item) => (
            <BreadcrumbItem key={item}>
              <BreadcrumbLink href={`/${item.toLowerCase()}`} aria-label={`Navigate to ${item}`}>
                {item}
              </BreadcrumbLink>
            </BreadcrumbItem>
          ))}
        </Breadcrumb>
      </Flex>

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

        {/* Databox section (WAS NOT ABLE TO IMPLEMENT)
        <Center
          border="1px solid grey"
          padding="0.5rem"
          width="auto"
          margin={margin}
          height="15.0rem"
        >
          <Grid templateColumns="repeat(4, 1fr)" gap={5} width="100%">
            <Box height="100%">
              <Databox measurement="motor_data"/>
            </Box>
          </Grid>
        </Center>

        */}

        {/* Graphing */}
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