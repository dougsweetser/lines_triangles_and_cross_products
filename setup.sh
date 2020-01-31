# Based on tutorial: https://www.youtube.com/watch?v=skpiLtEN3yk
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
