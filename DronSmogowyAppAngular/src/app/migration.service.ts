import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MigrationService {

  constructor(private http:HttpClient ) {}

  onRunMigration(fromData: FormData){
    this.http.post('http://localhost:8080/angular.php',fromData).subscribe(data => {
      alert(data);
      });
    // this.http.post('http://localhost:8080/angular.php',{}).subscribe(data =>     { 
    //   alert(data);
    //  });
  }
}
