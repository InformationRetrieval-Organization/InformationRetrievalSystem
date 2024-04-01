"use client";
import React, { useState } from "react";
import { Button, Input } from "@nextui-org/react";
import { SearchIcon } from "../components/icons";
import ResultsList from "./components/ResultsList";

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

  const handleSearch = async () => {
    /*
    const response = await fetch(
      `https://your-api-url.com/search?query=${inputValue}`
    );
    const data = await response.json();

	setResults(data);
	*/

    // TODO: Implement the search functionality
    setResults(sample);
  };

  return (
    <section className="m-8">
      <div className="flex items-center gap-2">
        <Input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type to search..."
          size="sm"
          startContent={<SearchIcon size={18} />}
          type="search"
        />

        <Button color="primary" onClick={handleSearch}>
          Search
        </Button>
      </div>

      <ResultsList results={results} />
    </section>
  );
}
