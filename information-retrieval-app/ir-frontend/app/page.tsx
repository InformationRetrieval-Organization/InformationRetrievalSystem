"use client";
import React, { useState } from "react";
import { Button, Divider, Input } from "@nextui-org/react";
import { SearchIcon } from "../components/icons";
import ResultsList from "./components/ResultsList";
import AdvancedFilter from "./components/AdvancedFilter";

const sample: SearchResult[] = [
  {
    title: "Sample Result 1",
    subtitle: "Subtitle 1",
    link: "http://example.com/1",
    timestamp: "2022-01-01T00:00:00Z",
    content: "This is the content of Sample Result 1",
  },
  {
    title: "Sample Result 2",
    subtitle: "Subtitle 2",
    link: "http://example.com/2",
    timestamp: "2022-01-02T00:00:00Z",
    content: "This is the content of Sample Result 2",
  },
  {
    title: "Sample Result 3",
    subtitle: "Subtitle 3",
    link: "http://example.com/3",
    timestamp: "2022-01-03T00:00:00Z",
    content: "This is the content of Sample Result 3",
  },
];

export default function Home() {
  const [inputValue, setInputValue] = useState("");
  const [results, setResults] = useState<SearchResult[] | null>(null);
  const [filters, setFilters] = useState([{ operator: "AND", value: "" }]);

  const handleSearch = async () => {
    try {
      let url = `http://127.0.0.1:5000/search/vector-space?q=${inputValue}`;

      // if any filter is set, use boolean search
      if (filters.some((filter) => filter.value !== "")) {
        url = `http://127.0.0.1:5000/search/boolean?q=${inputValue}&filters=${JSON.stringify(filters)}`;
      }

      const response = await fetch(url);
      const data = await response.json();

      setResults(data);
    } catch (error) {
      console.error("Failed to fetch data:", error);
      // todo: Handle the error appropriately
      setResults(sample);
    }
  };

  return (
    <section className="flex flex-col gap-5 m-8">
      <div className="flex items-center gap-2">
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="search term"
          size="md"
          type="search"
        />

        <Button isIconOnly color="primary" variant="solid" size="lg" onClick={handleSearch}>
          <SearchIcon size={18} />
        </Button>
      </div>

      <AdvancedFilter filters={filters} setFilters={setFilters} />

      <Divider />

      <ResultsList results={results} />
    </section>
  );
}
