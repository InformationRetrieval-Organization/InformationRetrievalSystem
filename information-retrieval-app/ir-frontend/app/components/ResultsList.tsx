import React from "react";
import { Card, CardHeader, CardBody, Divider, Link } from "@nextui-org/react";

export default function ResultsList({ results }: { results: SearchResult[] | null }) {
    if (!results) {
        return null;
    }

    return (
        <div>
            {results.map((result, index) => (
                <Card key={index} className="mt-3">
                    <CardHeader className="flex gap-3">
                        <div className="flex flex-col">
                            <p className="text-md">
                                <Link
                                    isExternal
                                    showAnchorIcon
                                    href={result.link}
                                >
                                    {result.title}
                                </Link>
                            </p>
                            <p className="text-small text-default-500">{result.subtitle}</p>
                        </div>
                        <p>{result.timestamp}</p>
                    </CardHeader>
                    <CardBody>
                        <p>{result.content}</p>
                    </CardBody>
                </Card>
            ))}
        </div>
    );
}