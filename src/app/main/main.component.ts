import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss'],
})
export class MainComponent implements OnInit {
  imagePath = '';
  imgURL: any = '';
  message: any;

  constructor(public http: HttpClient) {}

  ngOnInit(): void {}

  preview(files: any) {
    if (files.length === 0) return;

    var mimeType = files[0].type;
    if (mimeType.match(/image\/*/) == null) {
      this.message = 'Only images are supported.';
      return;
    }

    var reader = new FileReader();
    this.imagePath = files;
    reader.readAsDataURL(files[0]);
    reader.onload = (_event) => {
      this.imgURL = reader.result;
    };
  }


  predictSolution(url: any) {
    console.log(url)
    // var x = 
    const formData = new FormData();
    formData.append('predict',url);
    this.http
      .post(environment.baseURL + 'predict', formData)
      .subscribe((res) => {
        console.log(res);
      });
  }
}
