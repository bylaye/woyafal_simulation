import React, { createContext, useState } from 'react';

// Créez le contexte
export const CompteurContext = createContext();

// Créez un fournisseur de contexte
export const CompteurProvider = ({ children }) => {
    const [selectedCompteur, setSelectedCompteur] = useState(null);

    return (
        <CompteurContext.Provider value={{ selectedCompteur, setSelectedCompteur }}>
            {children}
        </CompteurContext.Provider>
    );
};
