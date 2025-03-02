The Backend is Fast API and not Node. There is a node file, so if you run npm start,
it will work because there is a connected node backend, but instead run
uvicorn app:app --reload.

You can use npm start for the frontend.
