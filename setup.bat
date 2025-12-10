cd frontend
CALL npm install
cd ../
cd backend
py -m venv myenv
CALL myenv\Scripts\activate
echo 'activated'
pip install -r requirements.txt
echo 'installed'
pause