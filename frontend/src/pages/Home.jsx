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

import { useParams } from "react-router-dom";
import LineChart from "../components/Chart";
import Config from "../components/Config";
import Collapsible from "../components/chat/Collapsible";
import DataUploader from "../components/chat/DataUploader";
import Chat from "../components/chat/Chat";
import NavBar from "../components/NavBar";

function Home() {
  const { extension } = useParams();
  const component = extension
    ? extension.charAt(0).toUpperCase() + extension.slice(1)
    : "";
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
      {/* navbar */}
      <NavBar />
      {/* Main content */}
      <Flex className="row">
        {/* collapsable */}
        <Collapsible
          title="Chat with your data"
          children={
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
                width: '100%',
                gap: '12px'
              }}
            >
              <DataUploader />
              <Chat />
            </div>
          }
        />
        {/* Data */}
        <Flex
          direction="column"
          flex="1"
          padding={margin}
        >
          {/* Title */}
          <Text fontSize="1.25rem">
            {component} Management
          </Text>
          {/* Config Component */}
          <Config onChange={handleConfigSelectionChange} />{" "}
          {/* Pass handler to Config */}
          {/* Graphing */}
          <Center
            border="1px solid grey"
            width="auto"
            flex="1"
            maxHeight="100.0rem"
          >
            <LineChart selectedConfig={selectedConfig} />{" "}
            {/* Pass selectedConfig to LineChart */}
          </Center>
        </Flex>
      </Flex>
    </Flex>
  );
}

export default Home;
