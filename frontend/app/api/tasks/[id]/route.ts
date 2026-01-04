import { NextRequest } from 'next/server'

export async function GET(request: NextRequest, { params }: { params: { id: string } }) {
  // Get the backend API URL from environment variables
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000'

  // Get the authorization header from the incoming request
  const authHeader = request.headers.get('authorization')

  try {
    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/tasks/${params.id}`, {
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
    console.error('Task GET API route error:', error)
    return new Response(JSON.stringify({ detail: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}

export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  // Get the backend API URL from environment variables
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000'

  // Get the authorization header from the incoming request
  const authHeader = request.headers.get('authorization')

  try {
    // Get the request body
    const body = await request.json()

    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/tasks/${params.id}`, {
      method: 'PUT',
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
    console.error('Task PUT API route error:', error)
    return new Response(JSON.stringify({ detail: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  // Get the backend API URL from environment variables
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000'

  // Get the authorization header from the incoming request
  const authHeader = request.headers.get('authorization')

  try {
    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/tasks/${params.id}`, {
      method: 'DELETE',
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
    console.error('Task DELETE API route error:', error)
    return new Response(JSON.stringify({ detail: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}

export async function PATCH(request: NextRequest, { params }: { params: { id: string } }) {
  // Get the backend API URL from environment variables
  const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000'

  // Get the authorization header from the incoming request
  const authHeader = request.headers.get('authorization')

  try {
    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/tasks/${params.id}/toggle`, {
      method: 'PATCH',
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
    console.error('Task PATCH API route error:', error)
    return new Response(JSON.stringify({ detail: 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}