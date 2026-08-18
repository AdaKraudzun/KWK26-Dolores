import gradio as gr
from huggingface_hub import InferenceClient

from sentence_transformers import SentenceTransformer
import torch




with open("knowledge.txt", "r", encoding="utf-8") as file:
  # Read the entire contents of the file and store it in a variable
  knowledge_text = file.read()

client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", bill_to="kode-with-klossy")


def preprocess_text(text):
  # Strip extra whitespace from the beginning and the end of the text
  cleaned_text = text.strip()

  # Split the cleaned_text by every newline character (\n)
  chunks = cleaned_text.split("\n")

  # Create an empty list to store cleaned chunks
  cleaned_chunks = []

  # Write your for-in loop below to clean each chunk and add it to the cleaned_chunks list
  for chunk in chunks:
    stripped_chunk = chunk.strip()
    if len(stripped_chunk) > 0:
      cleaned_chunks.append(stripped_chunk)

  # Print cleaned_chunks
  print(cleaned_chunks)

  # Print the length of cleaned_chunks
  print(len(cleaned_chunks))

  # Return the cleaned_chunks
  return cleaned_chunks




# Call the preprocess_text function and store the result in a cleaned_chunks variable
cleaned_chunks = preprocess_text(knowledge_text) # Complete this line
  



#TRYIT4

from huggingface_hub import create_discussion
# Load the pre-trained embedding model that converts text to vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(text_chunks):
  # Convert each text chunk into a vector embedding and store as a tensor
  chunk_embeddings = model.encode(text_chunks, convert_to_tensor=True) # Replace ... with the text_chunks list

  # Return the chunk_embeddings
  return chunk_embeddings

# Call the create_embeddings function and store the result in a new chunk_embeddings variable
chunk_embeddings = create_embeddings(cleaned_chunks) # Complete this line

#TRYIT 5

# Define a function to find the most relevant text chunks for a given query, chunk_embeddings, and text_chunks
def get_top_chunks(query, chunk_embeddings, text_chunks):
  # Convert the query text into a vector embedding
  query_embedding = model.encode(query, convert_to_tensor=True) # Complete this line

  # Normalize the query embedding to unit length for accurate similarity comparison
  query_embedding_normalized = query_embedding / query_embedding.norm()

  # Normalize all chunk embeddings to unit length for consistent comparison
  chunk_embeddings_normalized = chunk_embeddings / chunk_embeddings.norm(dim=1, keepdim=True)

  # Calculate cosine similarity between all chunks and the query using matrix multiplication
  similarities = torch.matmul(chunk_embeddings_normalized, query_embedding_normalized) # Complete this line

  # Print the similarities
  print(similarities)

  # Find the indices of the 3 chunks with highest similarity scores
  top_indices = torch.topk(similarities, k=3).indices

  # Print the top indices
  print(top_indices)

  # Create an empty list to store the most relevant chunks
  top_chunks = []

  # Loop through the top indices and retrieve the corresponding text chunks
  for index in top_indices:
    chunk = text_chunks[index]
    top_chunks.append(chunk)

  # Return the list of most relevant chunks
  return top_chunks

#TRYIT6

# Call the get_top_chunks function with the original query






#CHATBOT
def respond(message, history):
    dolores_chunks = get_top_chunks(message, chunk_embeddings, cleaned_chunks)
    dolores_info = "\n".join(dolores_chunks)
    
    messages = [{"role": "system", "content": f"You are Dolores. You are a helpful friendly chatbot who gives advice to women who experience economic mistreatment. Give accurate answers. Keep your answers at a maximum of four sentences per message. Base your response on the provided context {dolores_info}"}]

    if history:
        messages.extend(history)
    
    messages.append({"role": "user", "content": message}) 

    response = client.chat_completion(
        messages,
        max_tokens=300
    )
    # Complete this line

    return response.choices[0].message.content.strip()

#welcome_chatbot = gr.Chatbot(
    #value=[{"role": "assistant", "content": "Hello! I am Dolores. How can I help you today?"}]
#)

custom_theme = gr.themes.Soft(
    primary_hue = "emerald",
    secondary_hue = "green",
    neutral_hue = "purple",
    radius_size = "lg",
    font = [gr.themes.GoogleFont("Poppins"), "Arial", "sans-serif"]
    
)

with gr.Blocks(theme = custom_theme) as chatbot:
    gr.ChatInterface(
        respond,
        title = "Dolores",
        editable = True,
        description = "Hi, I'm Dolores, your personal AI assistant that specializes in helping women and gender minorities deal with economic mistreatment in the workplace. Whether it's drafting an email to your superiors or helping you navigate through local laws, I am here to support you every step of the way. Try inputing one of the sample prompts, or feel free to ask me anything!",
        examples = ["I’m a senior analyst at my company but my boss refuses to give me a raise even though my male colleagues have all received some. How can I bring this up to HR?", "How can I negotiate for better pay?", "How can I tell if I am experiencing economic abuse?", "What are laws that I should be aware of if I believe I am facing financial abuse due to my gender?" ]
    )

#chatbot = gr.ChatInterface(respond)

# THIS IS WHERE THE NEW CODE STARTS ---------------------------------------------------------------

    # CODE FOR QUICK LINKS AND RESOURCES
    # THIS IS 1 ROW WITH 2 COLUMNS
    gr.Markdown("---") # THIS IS JUST A VISUAL DIVIDER LINE FEEL FREE TO REMOVE
    gr.Markdown("## Quick Links & Other Resources") # YOUR TITLE

    with gr.Row(): # THIS CONTAINS YOUR RESOURCES + 2 COLUMNS, IF YOU DON'T WANT COLUMNS, JUST KEEP EVERYTHING UNDER THE ROW (this line)
        with gr.Column(): # FIRST BLOCK
            gr.Markdown("""
            ### Legal Resources
            * [Women's Law](https://www.womenslaw.org/) - Provides specific legal information and priority assistance via email to women and gender minorities
            * [National Domestic Violence Hotline](https://www.thehotline.org) - Call  800-799-7223 or text BEGIN to 88788 to recieve priority support and knowledge about dealing with economic mistreatment in the workplace.
            """)

        with gr.Column(): # SECOND BLOCK
            gr.Markdown("""
            ### Financial Support & Toolkits
            * [NNEDV](https://nnedv.org) - Toolkit that includes information about financial literacy and provides free resources for victims of economic abuse in the workplace and advocates fighting against it
            * [Allstate Mobile](https://www.allstatecorporation.com/the-allstate-foundation/relationship-abuse.aspx#:~:text=Disrupt%20the%20cycle%20of%20relationship,live%20free%20from%20relationship%20abuse.) - Empowers youth and victims by providing advice to disrupt the cycle of economic abuse in the workplace while also investing in nonprofit leaders
            """)

chatbot.launch(share=True, debug=True)


# TODO: This is just a starting point! Customize the system prompt,
# the model, and the interface to make this project your own!
