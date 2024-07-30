-- Table structure for table `user`
CREATE TABLE `user` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `rid` int NOT NULL,
  `fname` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `lname` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `gender` int NOT NULL,
  `tel` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `passwd` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `status` ENUM('sender', 'receiver') NOT NULL DEFAULT 'sender',
  PRIMARY KEY (`uid`),
  KEY `rid` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Constraints for table `user`
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`rid`) REFERENCES `role` (`rid`) ON DELETE CASCADE ON UPDATE CASCADE;

-- AUTO_INCREMENT for table `user`
ALTER TABLE `user`
  MODIFY `uid` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;



