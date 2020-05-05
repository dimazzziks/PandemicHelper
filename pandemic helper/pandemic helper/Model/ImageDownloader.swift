//
//  ImageDownloader.swift
//  pandemic helper
//
//  Created by Дмитрий on 04.05.2020.
//  Copyright © 2020 Dmitriy. All rights reserved.
//

import Foundation
import UIKit
func downloadImage(urlStr : String) -> UIImage {
    var image = UIImage(named: "rbc")
    
    guard let url = URL(string: urlStr) else {return image!}
    let task = URLSession.shared.dataTask(with: url) { (data, response, erorr) in
        guard let data = data else {return}
        print("chicl = dskfm")
        image =  UIImage(data: data)
        }
    task.resume()
    return image!
}
