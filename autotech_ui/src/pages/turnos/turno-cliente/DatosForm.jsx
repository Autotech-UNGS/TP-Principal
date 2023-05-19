import * as React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import turno from '../turno'
import Stack from '@mui/material/Stack';

//Acá obtengo tipo de turno, kilometraje y patente

function TipoDeTurno() {
    const [kmInput, setKmInput] = React.useState('');

    const handleClick = (event) => {
        setKmInput(event.target.value);
    };

    const guardarCambio = (event) => {
        const { value } = event.target;
        turno.tipo = value;
        console.log('Tipo de turno cargado en el json:', turno.tipo);
    };

    return (
        <FormControl>
            <FormLabel id="demo-controlled-radio-buttons-group">Tipo de turno</FormLabel>
            <Stack spacing={3} width={300}>
                <RadioGroup
                    aria-labelledby="demo-controlled-radio-buttons-group"
                    name="tipo"
                    onChange={guardarCambio}
                >
                    <FormControlLabel
                        value="evaluacion"
                        control={<Radio />}
                        label="Evaluacion"
                        onClick={handleClick}
                    />
                    <FormControlLabel
                        value="service"
                        control={<Radio />}
                        label="Service"
                        onClick={handleClick}
                    />
                    <br></br>
                    {kmInput === 'service' && <Kilometraje />}
                </RadioGroup>
            </Stack>
        </FormControl>
    );
}

//Esto se muestra solo en caso de que ponga service
class Kilometraje extends React.Component {
    state = { kilometros: '' };

    updateNumber = (e) => {
        const val = e.target.value;

        if (e.target.validity.valid) {
            this.setState({ kilometros: e.target.value });
            if (val > 200000) {
                turno.frecuencia_km = 200000;
            } else {
                turno.frecuencia_km = Math.ceil(val / 5000) * 5000;
            }
            console.log('frecuencia_km cargado en el json:', turno.frecuencia_km)
        }
        else if (val === '') this.setState({ kilometros: val });

    }

    render() {
        return (
            <FormControl fullWidth>
                <FormLabel id="demo-radio-buttons-group-label">Kilometraje actual:</FormLabel>
                <input
                    type='tel'
                    value={this.state.kilometros}
                    onChange={this.updateNumber}
                    pattern="[1-9][0-9]*"
                />
            </FormControl>
        );
    }
}

function Patente() {
    const handleChange = (event) => {
        const { value } = event.target;
        turno.patente = value;
        console.log('Patente cargada en el json:', turno.patente);
    };

    return (
        <TextField
            required
            id="patente"
            name="patente"
            label="Patente"
            fullWidth
            variant="outlined"
            inputProps={{ minLength: 6, maxLength: 7 }}
            onChange={handleChange}
        />
    )
}

export default function DatosForm() {
    return (
        <React.Fragment>
            <Typography variant="h6" gutterBottom>
                Patente y motivo del turno
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                    <Patente />
                </Grid>
                <Grid item xs={12}>
                    <TipoDeTurno />
                </Grid>
            </Grid>
        </React.Fragment>
    );
}
