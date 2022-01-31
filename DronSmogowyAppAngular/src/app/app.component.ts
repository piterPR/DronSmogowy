import { UiService } from './ui.service';
import { ChartComponent } from './main/chart/chart.component';
import { Component, ViewChild } from '@angular/core';
// import { MigrationService } from './migration.service';

declare var ol: any;

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {


  @ViewChild(ChartComponent) chart: ChartComponent | null = null;

  constructor(private ui: UiService) {

  }
 
  ngAfterViewInit(): void {
    if (this.chart) {
      this.ui.setChartComponent(this.chart);
    }
  }



}