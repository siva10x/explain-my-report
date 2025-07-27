# from langchain_openai import ChatOpenAI
# from langchain.prompts import PromptTemplate
# import os

# def explain_medical_text(text):
#     """Use LangChain and OpenAI to simplify medical text, focusing on prescription details."""
#     # Initialize OpenAI model
#     llm = ChatOpenAI(
#         model="gpt-4o",
#         api_key=os.getenv('OPENAI_API_KEY'),
#         temperature=0.7
#     )
    
#     # Split text into lines/sentences
#     segments = [line.strip() for line in text.split('\n') if line.strip() and any(keyword in line.lower() for keyword in ['medicine', 'dosage', 'duration', 'tab', 'cap'])]
    
#     # Create prompt template focused on prescription
#     prompt = PromptTemplate(
#         input_variables=["text"],
#         template="""
#         You are a medical assistant explaining prescription details to a patient with no medical background.
#         Simplify the following prescription text into plain, easy-to-understand English in one sentence, focusing only on the medicines, dosages, and how to take them.
#         Prescription text: {text}
#         Simplified explanation:
#         """
#     )
    
#     explanations = []
    
#     # Process each segment synchronously
#     for segment in segments:
#         try:
#             response = llm.invoke(prompt.format(text=segment))
#             simplified = response.content.strip().replace('Simplified explanation:', '').strip()
#             explanations.append({
#                 'original': segment,
#                 'simplified': simplified
#             })
#         except Exception as e:
#             explanations.append({
#                 'original': segment,
#                 'simplified': f"Error processing this line: {str(e)}"
#             })
    
#     return explanations


from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os

def explain_medical_text(text, prompt_type='general'):
    """Use LangChain and OpenAI to simplify medical text based on the prompt type."""
    # Initialize OpenAI model
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=os.getenv('OPENAI_API_KEY'),
        temperature=0.5  # Lowered to 0.5 for more consistent and precise output
    )
    
    # Split text into lines/sentences, ensuring single-line input is processed
    segments = [seg.strip() for seg in text.split('\n') if seg.strip()]
    if not segments:  # If no lines after split, treat the entire text as one segment
        segments = [text.strip()]
    
    # Define prompt templates based on type
    if prompt_type == 'prescription':
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            You are a highly skilled medical assistant tasked with explaining prescription details to a patient with no medical background. 
            Your goal is to provide a clear, concise, and empathetic explanation in one sentence, focusing solely on the medicines, dosages, and instructions (e.g., timing or food relation). 
            If the text is incomplete, ambiguous, or contains non-prescription details (e.g., doctor names), ignore those and focus only on extractable prescription information. 
            Avoid medical jargon and ensure the language is simple and actionable. 
            Text: {text}
            Simplified explanation:
            """
        )
    elif prompt_type == 'diagnosis':
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            You are a highly skilled medical assistant explaining medical diagnosis text to a patient with no medical background. 
            Provide a clear, concise, and reassuring explanation in one sentence, focusing on the condition, its basic meaning, and its general implications for the patient’s health (e.g., need for treatment or monitoring). 
            If the text is incomplete or unclear, offer a general simplification based on the available information and avoid speculation. 
            Use simple, non-technical language and an empathetic tone. 
            Text: {text}
            Simplified explanation:
            """
        )
    elif prompt_type == 'query':
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            You are a highly skilled medical assistant explaining general medical terms or queries to a patient with no medical background. 
            Provide a clear, concise, and friendly explanation in one sentence, defining the term or answering the query with practical, easy-to-understand information relevant to the patient’s daily life. 
            If the text is vague or unclear, make a reasonable assumption about the intent and provide a helpful response, avoiding complex medical terminology. 
            Text: {text}
            Simplified explanation:
            """
        )
    else:  # Default for unexpected prompt_type
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            You are a highly skilled medical assistant explaining complex medical text to a patient with no medical background. 
            Provide a clear, concise, and empathetic explanation in one sentence, simplifying the text into plain, easy-to-understand English. 
            If the text is unclear or unrelated to medicine, offer a general simplification or indicate it’s not applicable. 
            Text: {text}
            Simplified explanation:
            """
        )
    
    explanations = []
    
    # Process each segment
    for segment in segments:
        try:
            response = llm.invoke(prompt.format(text=segment))
            simplified = response.content.strip().replace('Simplified explanation:', '').strip()
            if simplified:  # Only add if there's a valid simplification
                explanations.append({
                    'original': segment,
                    'simplified': simplified
                })
        except Exception as e:
            explanations.append({
                'original': segment,
                'simplified': f"Error processing this line: {str(e)}"
            })
    
    return explanations