import { Injectable } from '@angular/core';
import { ChartComponent } from './main/chart/chart.component';


@Injectable({
  providedIn: 'root'
})
export class UiService {

  private names: any = undefined;
  confirmComponent: ChartComponent | null = null;

  constructor() {
  }

  setChartComponent(component: ChartComponent)
  {
    this.confirmComponent = component;
  }

  async wantToContinue(context: string, change?: boolean)
  {
    if(this.confirmComponent === null || this.confirmComponent === undefined) return false; 
    return new Promise<boolean>((resolve) => {
      if (change === undefined || (change !== undefined && change === true))
      {
        this.confirmComponent!.awaitToDecision(context).then(res => {
          resolve(res);
        });
      }
      else
      {
          resolve(true);
      }
    });
  }
}
