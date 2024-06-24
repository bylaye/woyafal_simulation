import React, {useState, useEffect, useContext} from "react";
import audiobip from './bip.mp3';
import audioBipSubmit from './bip_long.mp3';
import CodeList from './CodeList';
import axios from "axios";
import {ENDPOINT_CREDIT_KW, ENDPOINT_NEW_RECHARGE} from "./myconf";
import { CompteurContext } from "./CompteurContext";

const Simulateur = () => {

    const [code, setCode] = useState('');
    const [codePrint, setCodePrint] = useState('');
    const [codeLoop, setCodeLoop] = useState('');
    const [codeHaut, setCodeHaut] = useState('');
    const [message, setMessage] = useState('');
    const [n, setn] = useState('1');
    const SUCCESS = 'Success';
    const FAILED = 'Failed';
    const LEN_CODE_UTILE = 3;
    const LEN_CODE_RECHARGE = 20;
    const CODE_LIST = CodeList();
    const { selectedCompteur } = useContext(CompteurContext);


    const beep = (son) => {
        try{
            const audio = new Audio(son);
            audio.play();
        } catch (error){
            console.log("Audio playback failed:", error);
        }
    };


    const handleButtonClick = (value) => {
        // setCode(prevCode => prevCode + value);
        beep(audiobip);
        const newCode = code + value;
        setCode(newCode);
        setCodePrint(newCode.slice(-8));
        setCodeHaut(code.length + 1);
    };


    const handleSubmit = async () =>{
        beep(audioBipSubmit);
        if (code.length === LEN_CODE_UTILE ){
            if ( CodeList().hasOwnProperty(code) ){
                setMessage(SUCCESS);
                const w = handleCodeUtile();
                console.log('qq ', w)
                setMessage();
            }
            else{
                setMessage(FAILED);
            }
        }else if (code.length === LEN_CODE_RECHARGE){
            if (selectedCompteur && selectedCompteur.numeroCompteur){
                const response = await axios.put(
                    `${ENDPOINT_NEW_RECHARGE}/${selectedCompteur.numeroCompteur}`,
                    {codeRecharge: code},
                    {headers: {'Content-Type': 'application/json'}},
                )
                console.log(response.data)
            }
            setMessage('ok ok');
        } 
        
        clearAllState();
        console.log(code);
    }


    const handleCodeUtile = async () => {
        try{
            if (selectedCompteur && selectedCompteur.numeroCompteur){
                const response = await axios.get(`${ENDPOINT_CREDIT_KW}/${selectedCompteur.numeroCompteur}`);
                console.log(response.data.totalKwDispo);
                setMessage(response.data.totalKwDispo +' kw');
                return response.data
            }
        }catch(error){
            console.log(error)
        }
    };


    const handleDelete = () => {
        // setCode(prevCode => prevCode.slice(0, -1));
        setMessage('');
        const newCode = code.slice(0, -1);
        setCode(newCode);
        setCodePrint(newCode.slice(-8));
        if (code.length > 0){
            setCodeHaut(code.length - 1);
        } else if (code.length === 0){
            setCodeHaut('');
            setCodeLoop('');
        }
    };


    const clearAllState = () => {
        setCode('');
        setCodePrint('');
        setCodeHaut('');
        setn('');
        setCodeLoop('');
    };


    // const getFormattedDate = () => {
    //     const today = new Date();
    //     const dd = String(today.getDate()).padStart(2, '0');
    //     const mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0
    //     const yyyy = today.getFullYear();
    //     return `${dd}-${mm}-${yyyy}`;
    // };


    // const getFormattedTime = () => {
    //     const today = new Date();
    //     const hh = String(today.getHours()).padStart(2, '0');
    //     const min = String(today.getMinutes()).padStart(2, '0');
    //     const ss = String(today.getSeconds()).padStart(2, '0');
    //     return `${hh}:${min}:${ss}`;
    // };


    // const loopScreenPrint = (stateCodeHaut, stateMessage, stateN) =>{
    //     setMessage(stateMessage);
    //     setCodeLoop(stateCodeHaut);
    //     setn(stateN);
    // }


    // useEffect(() => {
        
    //     if (message ===  SUCCESS) {
    //         // setMessage('CONNECT');
    //         const timer = setTimeout(() => {
    //             setMessage('100,12 Kwh');
    //         }, 1000);
    //         return () => clearTimeout(timer);
    //     }
    //     else if (message === FAILED) {
    //         const timer = setTimeout(() => {
    //             setMessage('ffailedd ');
    //         }, 1000);
    //         return () => clearTimeout(timer);   
    //     }
    // }, [message]);


    // useEffect(() => {
    //     const timer = setTimeout(() => {
    //         if (n === '1') {
    //             loopScreenPrint('091','1234', '2');
    //         } else if (n === '2') {
    //             loopScreenPrint('081','888,88', '3');
    //         }else if (n === '3'){
    //             loopScreenPrint('002',getFormattedTime(), '4');
    //         }
    //          else {
    //             setMessage(getFormattedDate());
    //             setCodeLoop('001');
    //             setn('1');
    //         }
    //     }, 2000);
    //     // console.log(`Timer: ${timer}, CodeHaut: ${codeHaut}, Message: ${message}`);
    //     return () => clearTimeout(timer);
    // }, [n]);


    return (    
        <div className="emulateur">
            {/* Ecran Affichage */}
            <div className="ecran-alerte"> 
                <div className="ecran">
                    <div className="ecran-1">
                        {codeHaut && <span className="code-haut">{codeHaut}</span>} 
                        { !code  && codeLoop && <span className="code-haut">{codeLoop}</span>}
                    </div>
                    <div className="ecran-2">
                        {code && <p className="saisie">{codePrint}</p> }
                        {!code && message && <p className="print-message">{message}</p>}
                    </div>
                    
                </div>
                
                {/* Niveau de charge et alerte sonore */}
                <div className="alerte"> 
                    <div className="clignotants">
                        <div className="niveau-alerte">
                            <div className="clignotant  signal-vert" ></div>
                            <div className="niveau-charge-description">
                                <span className="titre">Niveau de charge</span><br/>
                                <span className="element">Vert: Suffisant</span><br/>
                                <span className="element">Rouge : Faible</span><br/>
                                <span className="element">Flash : Trés faible</span>
                            </div>
                        </div>
                        <div className="alarme-son">
                            <div className="clignotant" ></div>
                            <div className="titre">Alarme</div>
                        </div>
                        <div className="info-proprietaire">
                            <h2>Sunu Woyafal</h2>
                            <h3>230V 50Hz</h3>
                            <span>Fabriqué au Sénégal: 2024</span> <br/>
                            <span>@bylaye - Abdoulaye Niang</span>

                        </div>
                    </div> 
                </div>
            </div>

            {/* Clavier de saisie */}
            <div className="clavier">
                <div className="touch">
                    <button onClick={() => handleButtonClick('1')}>1</button>
                    <button onClick={() => handleButtonClick('2')}>2</button>
                    <button onClick={() => handleButtonClick('3')}>3</button>
                </div>
                <div>
                    <button onClick={() => handleButtonClick('4')}>4</button>
                    <button onClick={() => handleButtonClick('5')}>5</button>
                    <button onClick={() => handleButtonClick('6')}>6</button>
                </div>
                <div>
                    <button onClick={() => handleButtonClick('7')}>7</button>
                    <button onClick={() => handleButtonClick('8')}>8</button>
                    <button onClick={() => handleButtonClick('9')}>9</button>
                </div>
                <div>
                    <button onClick={handleDelete}>supp</button>
                    <button onClick={() => handleButtonClick('0')}>0</button>
                    <button onClick={handleSubmit}>En</button>
                </div>
            </div>
        </div>
    );
};

export default Simulateur;