import { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8000'
  const backendEndpoint = `${backendUrl}/auth/register`

  console.log('=== Register API ===')
  console.log('Backend URL:', backendUrl)
  console.log('Full endpoint:', backendEndpoint)

  try {
    const body = await request.json()
    console.log('Request body:', body)

    console.log('Calling backend...')
    const response = await fetch(backendEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    console.log('Backend response status:', response.status)

    const data = await response.json()
    console.log('Backend response data:', data)

    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  } catch (error: any) {
    console.error('Register API route error:', error)
    console.error('Error message:', error.message)
    return new Response(JSON.stringify({ detail: error.message || 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}
