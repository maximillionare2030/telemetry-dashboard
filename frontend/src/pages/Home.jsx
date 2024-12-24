// Home.jsx
import React, { useState, useEffect } from "react";
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
import Header from "../components/Header";
import NavBar from "../components/NavBar";
import Databox from "../components/stats/Databox";
import Timeseries from "../components/stats/Timeseries";
import { fetchInfluxInfo } from "../api/api";

function Home() {
  const { extension } = useParams();
  const component = extension
    ? extension.charAt(0).toUpperCase() + extension.slice(1)
    : "";

  const [selectedConfig, setSelectedConfig] = useState(null);

  // fetch configuration from influx upon initialization
  useEffect(() => {
    const initializeConfig = async () => {
      try {
        const { info } = await fetchInfluxInfo();

        // check that measurements exist
        if (info?.measurements?.length > 0) {
          const firstMeasurement = info.measurements[0];
          const firstFields = info.fields[firstMeasurement] || [];
          
          // function to set the selected config
          setSelectedConfig({
            databases: {
              defaultDB: {
                isSelected: true,
                measurements: {
                  [firstMeasurement]: {
                    isSelected: true,
                    fields: firstFields.reduce((acc, field) => ({
                      ...acc,
                      [field]: { isSelected: true }
                    }), {})
                  }
                }
              }
            }
          });
        }
      } catch (error) {
        console.error('Error initializing config:', error);
      }
    };

    initializeConfig();
  }, []);

  return (
    <Flex width="100%" height="100vh">
      {/* navbar  */}
      <NavBar />
      
      {/* Main content wrapper */}
      <Flex 
        className="main-content-wrapper"
      >
        {/* header */}
        <Header />

        {/* Main content */}
        <Flex className="row">
          {/* collapsable */}
          <Collapsible
            title="Chat with your data"
            children={
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  height: "100%",
                  width: "100%",
                  gap: "4px",
                  backgroundColor: "#232325"
                }}
              >
                <DataUploader />
                <Chat />
              </div>
            }
          />

          {/* Statistics container*/}
          <Flex className="container main-content">
            {/* Title */}
            <div className="title" >{component} Management</div>
            {/* Statistics overview */}
            <Databox />
            {/* time series */}
            <Timeseries 
              selectedConfig={selectedConfig}
            />
          </Flex>
        </Flex>
      </Flex>
    </Flex>
  );
}

export default Home;
