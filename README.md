I.
- CVs files from https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- Storing Embeddings in a Vector Database: ChromaDB
- The task has been done using LlamaIndex.
  
Expected outcome:
1. The repository contains a straightforward web application that lists candidates. Users can click on any candidate to view detailed information and a summary of their profile.
2. Evaluate and rank candidates based on their resumes using a custom or default prompt. It leverages an LLM to assess each candidate’s suitability for a specific job category or role.





https://github.com/user-attachments/assets/61f6e265-1a42-4f44-80e5-c172174f997c





https://github.com/user-attachments/assets/52b8dcb8-18b0-428e-b1fa-c15982391f17




To run this app, open your terminal and execute:

streamlit run app.py

Inside app.py, there are two available methods — choose the one you want to use.
If you prefer to run the logic directly in the terminal (without the Streamlit interface), you can execute:

python main.py

II.
- Connected to PostgreSQL + pgvector via PGVectorStore.
- Created multiple tools (including a pre-built one), 
- Built a ReAct-style FunctionAgent, 
- Integrated everything properly into a live, interactive workflow



https://github.com/user-attachments/assets/bbdb3472-abb3-4583-bf94-baacbbf86265



https://github.com/user-attachments/assets/90a4b012-c923-4f4b-b971-d55b642771c2



https://github.com/user-attachments/assets/c378ff35-56ac-4468-a5de-ee0896223129



To run this app, open your terminal and execute:

python test_agent.py

