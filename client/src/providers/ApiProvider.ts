import React, { useContext } from 'react';
import { Api } from '../api';

const ApiContext = React.createContext<Api>(new Api(import.meta.env.VITE_API_URL));

export function useApi() {
  return useContext(ApiContext);
}

export default ApiContext.Provider;
