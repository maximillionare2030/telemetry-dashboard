import React from "react";
import { 
  Flex, 
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Center,
  Text,
  Grid,
  Box
} from "@chakra-ui/react";

import Databox from "./Databox";
import LineChart from "./Chart";



function Header({ component }) {

  // Helper function to capitalize the first letter


  const margin = "1.0rem";

  return (
    <Flex
      direction="column" 
      width="100%" 
      height="100vh" 
      bg="white"
      margin = "0"
      padding = "0"
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
          {['Summary', 'Power', 'Motor', 'Microcontroller'].map((item) => (
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

        {/* Databox section */}
        <Center
          border="1px solid grey"
          padding="0.5rem"
          width="auto"
          margin = {margin}
          height="15.0rem"
        >

          <Grid templateColumns="repeat(4, 1fr)" gap={5} width="100%">
            <Box height="100%">
              <Databox title="Voltage" value="12.0" unit="V" />
            </Box>
          </Grid>
        </Center>

        {/* Graphing */}
        <Center
          border="1px solid grey"
          padding="0.5rem"
          width="auto"
          flex="1"
          margin={margin}
        >
          <LineChart />
        </Center>
      </Flex>
    </Flex>
  );
}

export default Header;
