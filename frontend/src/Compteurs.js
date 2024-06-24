import React, {useState, useEffect, useContext} from "react";
import axios from "axios";
import { CompteurContext } from "./CompteurContext";
import { ENDPOINT_ALL_COMPTEUR } from "./myconf";


const Compteurs = () => {
    const [compteurs, setCompteurs] = useState([]);
    // const [selectedCompteur, setSelectedCompteur] = useState(null);
    const { selectedCompteur, setSelectedCompteur } = useContext(CompteurContext);
    
    // const handleAllCompteur = async () => {
    //     try{
    //         const response = await axios.get(ENDPOINT_ALL_COMPTEUR);
    //         setCompteurs(response.data)
    //     } catch (error){
    //         console.log(error);
    //     }
    // }

    useEffect(() => {
        const fetchCompteurs = async () => {
            try {
                const response = await axios.get(ENDPOINT_ALL_COMPTEUR);
                setCompteurs(response.data);
                console.log('Liste des compteurs:', response.data);
            } catch (error) {
                console.log(error);
            }
        };

        fetchCompteurs();
    }, []);


    const handleRowClick = (compteur) => {
        setSelectedCompteur(compteur);
        console.log('Compteur sélectionné:',compteur, compteur.numeroCompteur);
    };

    return(
        <div className="compteurs">
            {/* <div className="ajouter-compteur">
                <p>Ajouter un compteur</p>
            </div> */}
            <div className="list-compteur">
                <p>Liste des compteurs</p>
                {/* <button onClick={handleAllCompteur}>Liste des compteurs</button> */}
                {compteurs.length > 0 ? (
                    <table>
                        <thead>
                            <tr>
                                <th>Immatricule</th>
                                <th>Numéro Compteur</th>
                                <th>Propriètaire</th>
                                <th>Adresse</th>
                            </tr>
                        </thead>
                        <tbody>
                            {compteurs.map((compteur, index) => (
                                <tr key={index} onClick={() => handleRowClick(compteur)} 
                                    style={{ cursor: 'pointer', 
                                    backgroundColor: selectedCompteur === compteur ? 'lightgreen' : 'grey' }}>
                                    <td>{compteur.immatricule}</td>
                                    <td>{compteur.numeroCompteur}</td>
                                    <td>{compteur.nom.toUpperCase()}  {compteur.prenom}</td>
                                    <td>{compteur.adresse}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>Aucun compteurs...</p>
                )}


            </div>
        </div>
    )
}

export default Compteurs;