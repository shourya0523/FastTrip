import React from "react";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import ButtonGroup from "@mui/material/ButtonGroup";
import { Typography } from "@mui/material";

type GroupButtonProps = {
  count: number;
  onSelect: (index: number) => void;
  selectedIndex: number;
};

export default function GroupButton({
  count,
  onSelect,
  selectedIndex,
}: GroupButtonProps) {
  const flights = Array.from({ length: count }, (_, i) => `Flight ${i + 1}`);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        "& > *": {
          m: 1,
        },
      }}
    >
      <Typography variant="overline">Flight options for you</Typography>
      <ButtonGroup
        color="secondary"
        size="large"
        aria-label="Large button group"
      >
        {flights.map((flight, index) => (
          <Button
            color="secondary"
            variant={selectedIndex === index ? "contained" : "outlined"}
            onClick={() => onSelect(index)}
            key={index}
          >
            {flight}
          </Button>
        ))}
      </ButtonGroup>
    </Box>
  );
}
