import React, {useState, useEffect, useContext} from "react";
import { ENDPOINT_ALL_RECHARGE_COMPTEUR } from "./myconf";
import axios from "axios";
import { CompteurContext } from "./CompteurContext";

const Recharges = () => {
    const [recharges, setRecharges] = useState([]);
    const { selectedCompteur } = useContext(CompteurContext);


    const formatCodeRecharge = (codeRecharge) => {
        return  codeRecharge.replace(/(.{4})/g, '$1  ');
    }


    const checkRecharge = (status) => {
        if (status == true){
            return 'OK'
        }
        return 'A Faire'
    }


    const getFormattedDate = (datestr) => {
        const today = new Date(datestr);
        const dd = String(today.getDate()).padStart(2, '0');
        const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0
        const yyyy = today.getFullYear();
        const hh = String(today.getHours()).padStart(2, '0');
        const min = String(today.getMinutes()).padStart(2, '0');
        const ss = String(today.getSeconds()).padStart(2, '0');
        return `${dd}-${mm}-${yyyy} ${hh}:${min}`;
    };

    useEffect(() => {
        const fetchRecharge = async () => {
            if (selectedCompteur) {
                try {
                    console.log('ddd', selectedCompteur.numeroCompteur);
                    const response = await axios.get(
                        `${ENDPOINT_ALL_RECHARGE_COMPTEUR}/${selectedCompteur.numeroCompteur}`
                    );
                    setRecharges(response.data);
                    console.log('Liste des recharges:', response.data);
                } catch (error) {
                    console.log(error);
                }
            }
            
        };

        fetchRecharge();
    }, [selectedCompteur]);

    return (
        <div className="recharges">
            <h2> Mes Recharges</h2>
            {/* {selectedCompteur ? (<h2>Compteur Numero : {selectedCompteur.numeroCompteur}</h2>) : (<h2></h2>)} */}
            {selectedCompteur ? (
                <table>
                    <thead>
                        <tr>
                            <th>Date </th>
                            <th>Status</th>
                            <th>Montant</th>
                            <th>Total KW</th>
                            <th>Code Recharge</th>
                        </tr>
                    </thead>
                    {recharges.length > 0 ? (
                    <tbody>
                        {recharges.map((recharge, index) => (
                            <tr key={index}>
                                <td>{getFormattedDate(recharge.dateRecharge)}</td>
                                <td>{checkRecharge(recharge.statusRecharge)}</td>
                                <td>{recharge.montantRecharge} F Cfa</td>
                                <td>{recharge.quantiteRecharge} kw</td>
                                <td>{formatCodeRecharge(recharge.codeRecharge)}</td>
                            </tr>
                        ))}
                    </tbody>
                ) : (
                    <tbody>
                        <tr>
                            <td colSpan="5">Aucune recharge ...</td>
                        </tr>
                    </tbody>
                )}
                </table>
            ) : (
                <p>Sélectionnez un compteur pour lister ces recharges.</p>
            )}
        </div>
    )
}

export default Recharges;