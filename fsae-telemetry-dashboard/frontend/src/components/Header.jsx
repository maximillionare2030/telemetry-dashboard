import React from "react";
import { 
  Flex, 
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Box,
  Center,
  Text,
  Grid,
  GridItem
} from "@chakra-ui/react";
import Databox from "./Databox";

function Header() {
  const margin = "1.0rem";

  return (
    <Flex minHeight="100vh"> 
      <Box 
        width="10%" as="div" // Explicitly set the type
        bg="white" 
        border="1px solid grey"
        height="100%" 
        position="fixed" 
        left="0" 
        top="0"
      />
      
      {/* Main Content */}
      <Box 
        width="100%" 
        marginLeft={{ base: '10%', md: '2.5%' }}
      >
        <Flex
          as="nav"
          aria-label="breadcrumb"
          align="center"
          justify="space-between"
          wrap="wrap"
          border="1px solid grey"
          padding="0.2rem"
        >
          <Breadcrumb separator="/" fontSize="1.4rem">
            {['Summary', 'Power', 'Motor', 'Microcontroller'].map((item) => (
              <BreadcrumbItem key={item}>
                <BreadcrumbLink href={item} aria-label={`Navigate to ${item}`}>{item}</BreadcrumbLink>
              </BreadcrumbItem>
            ))}
          </Breadcrumb>
        </Flex>

        <Flex>
          <Box width="80%" bg="#f3f3f3" border="1px solid grey">
            <Text fontSize="1.5rem" margin={margin}>[Power] Management</Text>

            <Center margin={margin} border="1px solid grey" padding="0.5rem" width="auto">
              <Grid templateColumns="repeat(4, 1fr)" gap={5} width="100%">
                <Databox title="Voltage" value="12.0" unit="V" />
                <GridItem h="200px" bg="white" border="1px solid grey" />
                <GridItem h="200px" bg="white" border="1px solid grey" />
                <GridItem h="200px" bg="white" border="1px solid grey" />
              </Grid>
            </Center>

            <Center margin={margin} border="1px solid grey" padding="0.5rem" width="auto" height="50%">
              {/* Add your content here */}
            </Center>
          </Box>

          {/* Sidebar Modules */}
          <Box width="20%" border="1px solid grey" justifyContent="center">
            <Text fontSize="1.5rem" padding="1.0rem" textAlign="center">Modules</Text>

            <Grid templateRows="repeat(4, 1fr)" gap={5} width="100%" padding="0.8rem">
              <GridItem h="200px" bg="white" border="1px solid grey" />
              <GridItem h="200px" bg="white" border="1px solid grey" />
              <GridItem h="200px" bg="white" border="1px solid grey" />
              <GridItem h="200px" bg="white" border="1px solid grey" />
            </Grid>
          </Box>
        </Flex>
      </Box>
    </Flex>
  );
}

export default Header;
