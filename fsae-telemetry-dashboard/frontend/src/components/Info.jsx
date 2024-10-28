import React, { useState } from "react";
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


import { Button, Checkbox, Menu, MenuButton, MenuList, MenuItem } from '@chakra-ui/react';

import Databox from "./Databox";
import LineChart from "./Chart";



function Info({ component }) {

  component = component.charAt(0).toUpperCase() + component.slice(1)

  const margin = "1.0rem";
  const [selectedItems, setSelectedItems] = useState([]);

  const measurementOptions = ["Voltage", "Power", "Option 3", "Option 4"];

  const handleToggle = (option) => {
    setSelectedItems((prevSelected) =>
      prevSelected.includes(option)
        ? prevSelected.filter((item) => item !== option)
        : [...prevSelected, option]
    );
  };
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
            <Databox measurement="motor_data"/>
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
          maxHeight="100.0rem"
        >
          <LineChart component={component} selectedItems={selectedItems} /> {/* component and measurements pased to LineChart */}
        </Center>

        <Menu closeOnSelect={false}>
          <MenuButton 
          width="10%"
          ml="right"
          margin={margin}
          as={Button}>
            Select Measurements
          </MenuButton>
          <MenuList>
            {measurementOptions.map((option) => (
              <MenuItem key={option} closeOnSelect={false}>
                <Checkbox
                  isChecked={selectedItems.includes(option)}
                  onChange={() => handleToggle(option)}
                >
                  {option}
                </Checkbox>
              </MenuItem>
            ))}
          </MenuList>
        </Menu>

      </Flex>
    </Flex>
  );
}

export default Info;
