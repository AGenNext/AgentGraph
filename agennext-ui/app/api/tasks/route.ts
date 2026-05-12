import { NextResponse } from 'next/server';

export async function GET() {
  const res = await fetch('http://localhost:8001/tasks');
  const tasks = await res.json();
  return NextResponse.json(tasks);
}

export async function POST(request: Request) {
  const body = await request.json();
  const res = await fetch('http://localhost:8001/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const task = await res.json();
  return NextResponse.json(task);
}