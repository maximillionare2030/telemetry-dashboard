import React from "react";
import {
  Flex,
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
} from "@chakra-ui/react";

const NavBar = () => {
  return (
    <>
      {/* Breadcrumb navigation */}
      <Flex
        as="nav"
        aria-label="breadcrumb"
        align="center"
        justify="space-between"
        wrap="wrap"
        border="1px solid grey"
      >
        <Breadcrumb fontSize="xl" style={{ color: "#6B7280" }}>
          {["Power", "Motor", "Microcontroller"].map((item) => (
            <BreadcrumbItem
              key={item}
              style={{
                cursor: "pointer",
              }}
            >
              <BreadcrumbLink
                href={`/${item.toLowerCase()}`}
                aria-label={`Navigate to ${item}`}
                style={{
                  padding: "8px 16px",
                  borderRadius: "4px",
                  textDecoration: "none",
                  fontWeight: "800",
                  color: "gray",
                  ":hover": { color: "black" },
                }}
              >
                {item}
              </BreadcrumbLink>
            </BreadcrumbItem>
          ))}
        </Breadcrumb>
      </Flex>
    </>
  );
};

export default NavBar;
