import json
from groq import Groq
from tools.product_tools import search_products, get_product
from tools.order_tools import get_order
from tools.return_tools import evaluate_return
import re
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

tools = [

    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search products using filters like price, tags, size, and sale status.",
            "parameters": {
                "type": "object",
                "properties": {

                    "max_price": {
                        "type": "number"
                    },

                    "size": {
                        "type": "string"
                    },

                    "is_sale": {
                        "type": "boolean"
                    },

                    "tags": {
                        "type": "array",
                        "description": (
                            "Use simple single-word tags like "
                            "cocktail, modest, bridal, evening, sleeve, fitted."
                        ),
                        "items": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": "Get product details using product_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string"
                    }
                },
                "required": ["product_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Fetch order details using order_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string"
                    }
                },
                "required": ["order_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "evaluate_return",
            "description": "Evaluate return eligibility using return policies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string"
                    }
                },
                "required": ["order_id"]
            }
        }
    }

]

def execute_tool(tool_name, arguments):

    if tool_name == "search_products":
        return search_products(arguments)

    elif tool_name == "get_product":
        return get_product(arguments["product_id"])

    elif tool_name == "get_order":
        return get_order(arguments["order_id"])

    elif tool_name == "evaluate_return":
        return evaluate_return(arguments["order_id"])

    else:
        return {
            "error": "Unknown tool"
        }

def run_agent(user_query):

    messages = [

        {
            "role": "system",
            "content": (

                "You are a retail AI assistant.\n"

                "You must use tools whenever factual data is required.\n"

                "Do not hallucinate products, inventory, orders, or policies.\n"

                "Always use valid JSON arguments for tool calls.\n"

                "For product searches:\n"
                "- Use simple tags like cocktail, modest, bridal, evening, sleeve.\n"
                "- Never use phrases like 'cocktail dress' as tags.\n"
                "- Never pass empty strings.\n"

                "When responding:\n"
                "- Use clean numbered lists\n"
                "- Keep responses concise\n"
                "- Do not dump raw JSON\n"
                "- Make recommendations easy to read\n"

                "For every product recommendation include:\n"
                "- Product title\n"
                "- Current price\n"
                "- Original price if on sale\n"
                "- One short reason why it matches\n"

                "If no products are found, clearly say so.\n"

                "If tool results exist, DO NOT say products were unavailable."
            )
        },

        {
            "role": "user",
            "content": user_query
        }
    ]

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2
        )

    except Exception as e:

        return (
            "I encountered a temporary tool-calling issue. "
            "Please try again."
        )

    response_message = response.choices[0].message

    if response_message.tool_calls:

        tool_call = response_message.tool_calls[0]

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print(f"\nTOOL CALLED: {tool_name}")
        print(f"ARGUMENTS: {arguments}")


        tool_result = execute_tool(
            tool_name,
            arguments
        )

        print("\nTOOL RESULT:")
        print(f"Returned {len(tool_result)} products")


        messages.append(response_message)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": json.dumps(tool_result)
        })



        messages.append({

            "role": "system",

            "content": (

                "Generate a clean, professional, easy-to-read response.\n"

                "Use numbered lists.\n"

                "Use spacing between products.\n"

                "Do not generate large paragraphs.\n"

                "Keep the response visually clean.\n"

                "Mention why recommendations match the request.\n"

                "For returns, clearly explain the policy decision."
            )
        })

        try:

            final_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.3
            )

            return final_response.choices[0].message.content

        except Exception as e:

            return (
                "The tool executed successfully, "
                "but response formatting failed."
            )


    else:

     content = response_message.content

    function_match = re.search(
        r'get_product\\(\\{"product_id":\\s*"([^"]+)"\\}\\)',
        content
    )

    if function_match:

        product_id = function_match.group(1)

        tool_result = get_product(product_id)

        return (
            f"Product Details:\\n\\n"
            f"Title: {tool_result['title']}\\n"
            f"Vendor: {tool_result['vendor']}\\n"
            f"Price: ${tool_result['price']}\\n"
            f"Tags: {', '.join(tool_result['tags'])}\\n"
            f"Bestseller Score: {tool_result['bestseller_score']}"
        )

    return content
