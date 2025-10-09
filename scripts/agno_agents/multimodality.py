from agno.media import Image

from pydantic import BaseModel, Field
from typing import List, Optional

from agno.agent import Agent
from agno.models.google import Gemini

from dotenv import load_dotenv
load_dotenv()

class LineItem(BaseModel):
    description: str = Field(..., description="Description of the service or product")
    quantity: float = Field(..., description="Quantity of items or services")
    unit_price: float = Field(..., description="Price per unit in the invoice currency")
    total_price: float = Field(..., description="Total price for this line item (quantity × unit_price)")

class InvoiceData(BaseModel):
    vendor_name: str = Field(..., description="Company name of the vendor issuing the invoice")
    vendor_address: str = Field(..., description="Complete address of the vendor")
    vendor_email: Optional[str] = Field(None, description="Email address of the vendor if available")

    client_name: str = Field(..., description="Name of the client or company being billed")
    client_address: str = Field(..., description="Complete billing address of the client")

    line_items: List[LineItem] = Field(..., description="List of all services/products on the invoice with quantities and prices")

SYSTEM_PROMPT = """
You are an expert invoice processing assistant that extracts structured data from invoice images with high accuracy.

<getInvoiceDetails>
Extract all these key fields, some example includes:
- Vendor: name, address, contact info, tax ID
- Invoice: number, date, due date, PO number
- Billing: company name, address
- Line items: description, quantity, unit price, total
- Totals: subtotal, tax, discount, total due
- Payment terms and notes
</getInvoiceDetails>

<requirements>
Requirements:
- Maintain 95%+ accuracy for critical fields
- Use null for missing information
- Include confidence scores for uncertain data
- Flag low-quality images or unclear text
- Validate numerical calculations
- Handle multiple currencies and formats
- Adapt to various invoice layouts
</requirements>

<output>
Directly include the output in JSON format. Don't include any text before or after the JSON. No explaination needed
</output>
"""

INSTRUCTIONS = """
- Extract vendor information from top section
- Identify table boundaries for line items
- Validate mathematical accuracy
- Flag uncertain extractions with confidence scores
- Handle multiple languages and currencies
- Note any data quality issues
"""

agent = Agent(
    model = Gemini(id="gemini-2.5-flash"),
    role = "Expert Invoice analyzer who extracts structured data from invoice images",
    instructions = INSTRUCTIONS,
    system_message = SYSTEM_PROMPT,
    output_schema = InvoiceData,
    use_json_mode = True,
)

image_path = "image.jpg"

response = agent.run(
    "Extract details",
    images=[Image(filepath=image_path)],
    stream=False
)

print(response.content)