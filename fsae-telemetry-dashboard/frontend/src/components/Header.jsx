import React from "react";
import { 
  Flex, 
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  Box,
  Container,
  Center,
  Text,
  Grid,
  GridItem
} from "@chakra-ui/react";

function Header() {
  return (
    <Flex height="100vh"> {/* Set Flex to take full viewport height */}
      {/* Sidebar */}
      <Box 
        width="2.5%" 
        bg="white" 
        border="1px solid grey" 

        height="100%" // Ensure it takes full height
        position="fixed" // Make it fixed on the left
        left="0" // Align it to the left
        top="0" // Align it to the top
      >
        
      </Box>

      {/* Main Content */}
      <Box 
        width="100%" 
        marginLeft="2.5%"// Push content to the right of the sidebar
      >
        <Flex
          as="nav"
          align="center"
          justify="space-between"
          wrap="wrap"
          border="1px solid grey"
          padding="0.2rem"
        >
          <Breadcrumb separator="/" fontSize="1.4rem">
            <BreadcrumbItem>
              <BreadcrumbLink href='Summary'>Summary</BreadcrumbLink>
            </BreadcrumbItem>

            <BreadcrumbItem>
              <BreadcrumbLink href='Power'>Power</BreadcrumbLink>
            </BreadcrumbItem>

            <BreadcrumbItem>
              <BreadcrumbLink href='Motor'>Motor</BreadcrumbLink>
            </BreadcrumbItem>

            <BreadcrumbItem>
              <BreadcrumbLink href='Microcontroller'>Microcontroller</BreadcrumbLink>
            </BreadcrumbItem>
          </Breadcrumb>
        </Flex>

        <Flex>
         <Box width="80%" height="100vh" bg="#f3f3f3" border="1px solid grey" >
         <Text fontSize="1.5rem" margin="1.5rem 0 0 1.5rem">[Power] Management</Text>
         <Center margin="1.5rem 1.5rem 1.5rem 1.5rem" border="1px solid grey" padding="0.5rem" width="auto">
      <Grid templateColumns="repeat(4, 1fr)" gap={5} width="100%">
        <GridItem h="200px" bg="white.500" border="1px solid grey" />
        <GridItem h="200px" bg="white.500" border="1px solid grey" />
        <GridItem h="200px" bg="white.500" border="1px solid grey" />
        <GridItem h="200px" bg="white.500" border="1px solid grey" />
      </Grid>
    </Center>
       </Box>

       <Box width="20%" height="100vh" border="1px solid grey" >
         <Text></Text>
       </Box>
        </Flex>
       

      </Box>
    </Flex>
  );
}

export default Header;
