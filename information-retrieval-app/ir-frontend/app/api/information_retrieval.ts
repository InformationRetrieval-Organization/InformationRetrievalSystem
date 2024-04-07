const baseUrl = process.env.IR_API_URL;

export async function getData(url: string) {
    const response = await fetch(`${baseUrl}${url}`);
    return response.json();
}

export async function postData(url: string, body: object) {
    const response = await fetch(`${baseUrl}${url}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    return response.json();
}