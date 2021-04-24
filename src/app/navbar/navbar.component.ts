import { Component, OnInit } from '@angular/core';
import { CommonService } from '../common.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  navStatus = false;

  constructor(public commonService: CommonService) { }

  ngOnInit(): void {
  }

  toggle() {
    this.navStatus = !this.navStatus; 
  }

  navigateToGH() {
    window.location.href = "https://github.com/likhithnemani/handwritten-problem-solver";
  }

}
