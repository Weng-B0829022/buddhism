const useSnack = () => ({
    snacks: [] as Array<{id: string, message: string, type: 'success' | 'error' | 'warning'}>,
    showSnack: (message: string, type: 'success' | 'error' | 'warning' = 'success') => {
        console.log(`${type}: ${message}`);
    }
});

export default useSnack;