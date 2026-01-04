import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  // Get the backend API URL from environment variables
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000'

  // Get the authorization header from the incoming request
  const authHeader = request.headers.get('authorization')

  try {
    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/tasks/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authHeader || '',
      },
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
    console.error('Tasks GET API route error:', error)
    return new Response(JSON.stringify({ detail: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}

export async function POST(request: NextRequest) {
  // Get the backend API URL from environment variables
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000'

  // Get the authorization header from the incoming request
  const authHeader = request.headers.get('authorization')

  try {
    // Get the request body
    const body = await request.json()

    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/tasks/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authHeader || '',
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
    console.error('Tasks POST API route error:', error)
    return new Response(JSON.stringify({ detail: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}