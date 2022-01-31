export interface ScanData {
    cityName: string;
    cityPopulation: number;
    citySurfaceAreaInKilometerSquared: number;
    personDensityPerKilometer: number;

    airQuality: 'Dobra' | 'Średnia' | 'Zła';
    airScans: Array<object>;
    pm10: number;
    pm25: number;
    humidity: number;
    hPa: number;
    temperature: number;
    IAQ: number;
    time: string;
    
}