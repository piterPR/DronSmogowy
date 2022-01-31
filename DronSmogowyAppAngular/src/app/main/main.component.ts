import { UiService } from './../ui.service';
import { MigrationService } from './../migration.service';
import { Component, Input, OnInit } from '@angular/core';
import { ScanData } from './data.model';
import measurements from './chart/chart_data2.json';
import { ThrowStmt } from '@angular/compiler';
import { MapsModule } from '@syncfusion/ej2-angular-maps';
import { LegendService, MarkerService, MapsTooltipService, DataLabelService, BubbleService, NavigationLineService, SelectionService, AnnotationsService, ZoomService } from '@syncfusion/ej2-angular-maps';
import { Maps, Zoom, Marker, NavigationLine } from '@syncfusion/ej2-angular-maps';



declare var ol: any;

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {


  public scanedData: ScanData | undefined;
  public measurement:{
    pm10: number,
    pm25: number,
    humidity: number,
    hPa: number,
    temperature: number,
    IAQ: number,
    time: string
  } = measurements.measurements[measurements.measurements.length-1];
  latitude: number = 21.9970283;
  longitude: number = 50.036263;
  map: any;
  markerSettings: any;
  navigationLineSettings: any;
  response = ""

  constructor(private ui: UiService,private mig: MigrationService ) {
    
  }
  

  ngOnInit() {
    // this.map.Inject(Zoom,Marker,NavigationLine)
    this.map = new ol.Map({
      target: 'map',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([this.latitude, this.longitude]),
        zoom: 13
      })
    });
    this.markerSettings = [{
      visible: true,
      height: 25,
      width: 15,
      dataSource: [
          {
              latitude: 21.9970283,
              longitude: 50.036263,
              name: "Start"
              
          },
          {
              latitude: 21.989844423328677,
              longitude: 50.01901014521318,
              name: "End"
          }
      ]
    }]
    this.navigationLineSettings = [{
      visible: true,
      color: "blue",
      width: 5,
      angle: 0.1,
      latitude: [21.9970283, 21.989844423328677],
      longitude: [50.036263,50.01901014521318]
  }];
    this.getData();
    console.log(this.measurement)
  }

  getData() {

    const data: any = {
      cityName: 'Rzeszów',
      cityPopulation: 183901,
      citySurfaceAreaInKilometerSquared: 129,
      airScans: [],
      pm10: this.measurement.pm10,
      pm25: this.measurement.pm25,
      humidity: this.measurement.humidity,
      hPa: this.measurement.hPa,
      temperature: this.measurement.temperature,
      IAQ: this.measurement.IAQ
    }
    const personDensityPerKilometer = data.cityPopulation/data.citySurfaceAreaInKilometerSquared;
    
    this.scanedData = {...data, personDensityPerKilometer: personDensityPerKilometer, airQuality: data.iaq < 50 ? 'Dobra' : data.iaq < 100 ? 'Średnia' : 'Zła'}
  }

  openUrl(url: string) {
    window.open(url);
  }

  openChart() {
    this.ui.wantToContinue('chart');
  }


  runMigration(name:string) {
    const formData : FormData = new FormData()
    formData.append('name',name)
    this.mig.onRunMigration(formData)
    console.log("Run mig")
  }



  get todayDateString() {
    return new Date(this.measurement.time).toLocaleDateString();
  }

  riskDotPositionStyle(x: number, y: number, size: number) {
    return `top: ${x}px; left: ${y}px; width: ${size}rem; height: ${size}rem;`
  }
}
