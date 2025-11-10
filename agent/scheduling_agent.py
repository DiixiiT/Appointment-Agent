import json

import httpx
from openai import OpenAI

from agent.prompts import system_prompt
from rag.faq_rag import retrieve_insurance_info
from utility.constant import AVAILABLE_SLOT_URL, BOOKING_API_URL

client = OpenAI()

user_sessions = {}


async def book_appointment(
    appointment_type, date, start_time, reason, name, email, phone
):
    patient = {"name": name, "email": email, "phone": phone}
    payload = {
        "appointment_type": appointment_type,
        "patient": patient,
        "date": date,
        "start_time": start_time,
        "reason": reason,
    }
    print("SENDING request")
    async with httpx.AsyncClient() as client:
        header = {"Authorization": "Bearer hhvjgvg", "Content-Type": "application/json"}
        response = await client.post(
            BOOKING_API_URL,
            data=json.dumps(payload),
            headers=header,
        )
        return response.json()


async def get_available_slots(date_param):
    param = {"date_param": date_param}
    async with httpx.AsyncClient() as client:
        header = {"Authorization": "Bearer hhvjgvg", "Content-Type": "application/json"}
        response = await client.get(
            AVAILABLE_SLOT_URL,
            params=param,
            headers=header,
        )
        return response.json()


async def agentchat(session_id, user_message):

    if session_id not in user_sessions:
        user_sessions[session_id] = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

    messages = user_sessions[session_id]
    messages.append({"role": "user", "content": user_message})

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "book_appointment",
                    "description": "Book an appointment for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "date": {"type": "string"},
                            "start_time": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Start time of the appointment in ISO 8601 format, e.g., 2025-11-10T17:21:52.019000Z",
                            },
                            "appointment_type": {
                                "type": "string",
                                "description": "consultation | followup | physical | special",
                            },
                            "reason": {"type": "string"},
                            "phone": {"type": "string"},
                        },
                        "required": [
                            "appointment_type",
                            "date",
                            "start_time",
                            "reason",
                            "name",
                            "email",
                            "phone",
                        ],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_available_slots",
                    "description": "Fetch available slots for the clinic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date_param": {"type": "string"},
                            "appointment_type": {"type": "string"},
                        },
                        "required": ["date_param"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "retrieve_insurance_info",
                    "description": "Search insurance and policy database for relevant information",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"],
                    },
                },
            },
        ],
    )
    msg = completion.choices[0].message
    messages.append(msg)
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = tool_call.function.arguments
            tool_call_id = tool_call.id
            if func_name == "book_appointment":
                print("Calling boking API........")
                tool_call = msg.tool_calls[0]
                args = json.loads(tool_call.function.arguments)
                print("ARGS  : ", args)
                result = await book_appointment(
                    name=args["name"],
                    email=args["email"],
                    date=args["date"],
                    start_time=args["start_time"],
                    appointment_type=args["appointment_type"],
                    phone=args["phone"],
                    reason=args["reason"],
                )

                reply = f"✅ Appointment booked for {args['name']} ({args['email']}) on {args['date']} at {args['start_time']}."

                # messages.append({"role": "assistant", "content": confirmation})
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": reply,
                    }
                )

                # return {"response": confirmation, "api_result": result}
            elif func_name == "get_available_slots":
                args = json.loads(tool_call.function.arguments)
                slots = await get_available_slots(args["date_param"])
                available_slots = []
                for s in slots["availability_solts"]:
                    available_slots.append(
                        f'start_time : {s["start_time"]} end_time:{s["end_time"]}'
                        if s["availability"] == True
                        else ""
                    )
                reply = f"Here are available slots for {args['date_param']}: {', '.join(available_slots)}. Please choose one."
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call_id, "content": reply}
                )
                messages.append({"role": "assistant", "content": reply})

                return {"response": reply}
            elif func_name == "retrieve_insurance_info":
                args = json.loads(tool_call.function.arguments)
                reply = retrieve_insurance_info(args["query"])
                messages.append(
                    {"role": "tool", "tool_call_id": tool_call_id, "content": reply}
                )
            second_response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages
            )
            assistant_reply = second_response.choices[0].message.content
            return {"response": assistant_reply}

    return {"response": msg.content}
