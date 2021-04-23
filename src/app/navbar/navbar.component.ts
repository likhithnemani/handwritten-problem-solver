import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  navStatus = false;

  constructor() { }

  ngOnInit(): void {
  }

  toggle() {
    this.navStatus = !this.navStatus; 
  }

}
