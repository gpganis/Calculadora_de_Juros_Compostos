DROP TABLE IF EXISTS `tb_investimentos`;

CREATE TABLE IF NOT EXISTS `DataBase`.`tb_investimentos` (
  `Id_Investimento` INT NOT NULL AUTO_INCREMENT,
  `Porcentagem_ao_Ano` DECIMAL(15, 2) NOT NULL,
  `Período_em_Meses` INT NOT NULL,
  `Valor_Inicial` DECIMAL(15, 2) NOT NULL,
  `Aporte_Mensal` DECIMAL(15, 2) NOT NULL,
  `Investimento_Total` DECIMAL(15, 2) NOT NULL,
  `Patrimônio_Bruto` DECIMAL(15, 2) NOT NULL,
  `Rendimento_Bruto` DECIMAL(15, 2) NOT NULL,
  `Patrimônio_Líquido` DECIMAL(15, 2) NOT NULL,
  `Rendimento_Líquido` DECIMAL(15, 2) NOT NULL,
  PRIMARY KEY (`Id_Investimento`)
) ENGINE = InnoDB;