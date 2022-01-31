import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import measurements from './chart_data2.json';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnInit{

  options_pm10: any;
  options_pm25: any;
  options_humidity: any;
  options_hPa: any;
  options_temperature: any;
  options_iaq: any;
  public measurementList:{
    pm10: number,
    pm25: number,
    humidity: number,
    hPa: number,
    temperature: number,
    IAQ: number,
    time: string
  }[] = measurements.measurements;
  constructor() {

  }

  ngOnInit(): void {
    const xAxisData: string[] = [];
    const pm10: number[] = [];
    const pm25: number[] = [];
    const humidity: number[] = [];
    const hPa: number[] = [];
    const temperature: number[] = [];
    const IAQ: number[] = [];

    let today = new Date();
    this.measurementList.forEach(element => {
      let acurate = new Date(element.time);
      xAxisData.push(acurate.toLocaleDateString());
      pm10.push(parseFloat(element.pm10.toFixed(3)));
      pm25.push(parseFloat(element.pm25.toFixed(3)));
      humidity.push(parseFloat(element.humidity.toFixed(3)));
      hPa.push(parseFloat(element.hPa.toFixed(3)));
      temperature.push(parseFloat(element.temperature.toFixed(3)));
      IAQ.push(parseFloat(element.IAQ.toFixed(3)));
    });
  
    xAxisData.reverse();

    this.options_pm25 = {
      tooltip: {},
      xAxis: {
        data: xAxisData,
        silent: false,
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        name: "µg/m³"
      },
      series: [
        {
          name: 'PM 2,5',
          type: 'line',
          data: pm25,
          animationDelay: (idx: number) => idx * 10 + 300,
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: (idx: number) => idx * 5,
    };
    this.options_pm10 = {
      tooltip: {},
      xAxis: {
        data: xAxisData,
        silent: false,
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        name: "µg/m³"
      },
      series: [
        {
          name: 'PM 10',
          type: 'line',
          data: pm10,
          animationDelay: (idx: number) => idx * 10 + 300,
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: (idx: number) => idx * 5,
    };
    this.options_humidity = {
      tooltip: {},
      xAxis: {
        data: xAxisData,
          silent: false,
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        name: "%"
      },
      series: [
        {
          name: 'Humidity',
          type: 'line',
          data: humidity,
          animationDelay: (idx: number) => idx * 10 + 300,
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: (idx: number) => idx * 5,
    };
    this.options_hPa = {
      tooltip: {},
      xAxis: {
        data: xAxisData,
        silent: false,
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        name: "hPa"
      },
      series: [
        {
          name: 'Atmospheric pressure',
          type: 'line',
          data: hPa,
          animationDelay: (idx: number) => idx * 10 + 300,
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: (idx: number) => idx * 5,
    };
    this.options_temperature = {
      tooltip: {},
      xAxis: {
        data: xAxisData,
        silent: false,
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        name: "°C"
      },
      series: [
        {
          name: 'Temperature',
          type: 'line',
          data: temperature,
          animationDelay: (idx: number) => idx * 10 + 300,
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: (idx: number) => idx * 5,
    };
    this.options_iaq = {
      tooltip: {},
      xAxis: {
        data: xAxisData,
        silent: false,
        splitLine: {
          show: false,
        },
      },
      yAxis: {
        name: "µg/m³"
      },
      series: [
        {
          name: 'IAQ',
          type: 'line',
          data: IAQ,
          animationDelay: (idx: number) => idx * 10 + 300,
        }
      ],
      animationEasing: 'elasticOut',
      animationDelayUpdate: (idx: number) => idx * 5,
    };
  }

  context: string | null = null;

  @Output() decision = new EventEmitter<boolean>();

  async awaitToDecision(context: string)
  {
    this.context = context;
    // this.options = Object.assign(this.options);
    return new Promise<boolean>((resolve) => {
      this.decision.subscribe(event => {
        this.context = null;
        resolve(event);
      });
    });
  }

  decide(value: boolean)
  {
    this.decision.emit(value);
  }

  dummy(event: Event) {
    event.stopPropagation();
  }
}
