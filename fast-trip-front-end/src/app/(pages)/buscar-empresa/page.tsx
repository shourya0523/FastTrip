"use client";

import Space from "@/app/components/space/Space";
import { Typography } from "@mui/material";
import Card from "@/app/components/card/Card";
import companies from "@/app/mocks/companies.json";
import Pagination from "@/app/components/pagination/Pagination";
import Stack from "@mui/material/Stack";
import Breadcrumb from "@/app/components/breadcrumb/Breadcrumb";
import HideOnDesktop from "@/app/components/hideOnDesktop/HideOnDesktop";
import SearchBar from "@/app/components/search-bar/SearchBar";
import { ROUTE } from "@/app/types/generic";
import { useRouter } from "next/navigation";

export default function Companies() {
  const router = useRouter();
  const handleSearch = (search: string) => {
    router.push(`/${ROUTE.BUSCAR_EMPRESA}?search=${search}`);
  };

  return (
    <>
      <Space top={6} />
      <Stack spacing={2}>
        <Breadcrumb />
        <Typography
          variant="title"
          fontWeight="bold"
          sx={{
            fontSize: {
              xs: "28px",
            },
            lineHeight: {
              xs: "28px",
            },
          }}
        >
          Empresas encontradas <span className="text-[#007E50]">(2102)</span>
        </Typography>
        <HideOnDesktop>
          <SearchBar onSearch={handleSearch} stickyOnScroll />
        </HideOnDesktop>
        <ul className="flex flex-wrap max-md:w-full ">
          {companies.map((item, index) => (
            <Card
              key={index}
              name={item.name}
              nationalRegistry={item.nationalRegistry}
              websiteUrl={item.websiteUrl}
              imageSrc={item.imageSrc}
              slug={item.slug}
            />
          ))}
        </ul>
        <div className="flex justify-center">
          <Pagination count={10} variant="outlined" shape="rounded" />
        </div>
      </Stack>
    </>
  );
}
