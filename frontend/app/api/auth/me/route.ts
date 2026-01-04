import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const backendUrl = process.env.BACKEND_API_URL || 'http://127.0.0.1:8000'
  const authHeader = request.headers.get('authorization')

  try {
    const response = await fetch(`${backendUrl}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': authHeader || '',
      },
    })

    const data = await response.json()

    return new Response(JSON.stringify(data), {
      status: response.status,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  } catch (error: any) {
    console.error('Me API route error:', error)
    return new Response(JSON.stringify({ detail: error.message || 'Internal server error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }
}
