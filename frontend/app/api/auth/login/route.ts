import { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  // Get the backend API URL from environment variables
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000'

  try {
    // Get the request body
    const body = await request.json()

    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    // Get the response data
    const data = await response.json()

    // Return the response
    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  } catch (error) {
    console.error('Login API route error:', error)
    return new Response(JSON.stringify({ detail: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}