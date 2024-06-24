import './App.css';
import Simulateur from './Simulateur';
import Compteurs from './Compteurs';
import Recharges from './Recharges';
import { CompteurProvider } from './CompteurContext';

function App() {


  return (
    <div className="App">
      

        <CompteurProvider>
          <div>
            <h2> Numero Compteur {} </h2>
            {/* {compteur} */}
          </div>
          <div className='App1'>
            <Compteurs />           
            <Recharges />
          </div>
          <div className='App2'>
            <Simulateur />
          </div>
        </CompteurProvider>

    </div>
  );
}

export default App;
