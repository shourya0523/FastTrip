"use client";

import { Typography } from "@mui/material";
import FacebookIcon from "@mui/icons-material/Facebook";
import InstagramIcon from "@mui/icons-material/Instagram";
import LinkedInIcon from "@mui/icons-material/LinkedIn";

export default function Footer() {
  return (
    <footer
      className={` mt-12  w-full bottom-0 flex items-center justify-between px-[160px] max-md:px-4 border-t border-lightGrey h-[80px] bg-white max-md:flex-col-reverse max-md:justify-evenly`}
      aria-label="Rodapé do site Datapanp"
    >
      <Typography variant="body1" color="darkGrey">
        Fast Trip © 2025 – All rights reserved.
      </Typography>

      <nav
        className="flex gap-4 items-center"
        aria-label="Links para redes sociais"
      >
        <span
          aria-hidden="true"
          title="Facebook indisponível"
          className="opacity-30 cursor-not-allowed"
        >
          <FacebookIcon />
        </span>
        <span
          aria-hidden="true"
          title="Instagram indisponível"
          className="opacity-30 cursor-not-allowed"
        >
          <InstagramIcon />
        </span>
        <span
          aria-hidden="true"
          className="opacity-30 cursor-not-allowed"
          rel="noopener noreferrer"
          aria-label="Ir para o LinkedIn da Datapanp"
        >
          <LinkedInIcon className="cursor-pointer" />
        </span>
      </nav>
    </footer>
  );
}
